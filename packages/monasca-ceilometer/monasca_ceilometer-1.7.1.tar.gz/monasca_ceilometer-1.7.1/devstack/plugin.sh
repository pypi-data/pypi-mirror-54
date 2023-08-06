# plugin.sh - DevStack plugin.sh dispatch script template

function install_ceilosca {
   echo "In install_ceilosca"
}

function init_ceilosca {
   echo "In init_ceilosca"
   get_or_add_user_project_role "monasca-user" "ceilometer" $SERVICE_PROJECT_NAME
}

function configure_ceilosca {
    echo "In configure_ceilosca"
    sudo mkdir -p /etc/ceilometer
    sudo chown $CEILOSCA_USER /etc/ceilometer
    # back up Ceilometer's ceilometer.conf for reference
    if [[ -e /etc/ceilometer/ceilometer.conf ]]; then
        cp /etc/ceilometer/ceilometer.conf /etc/ceilometer/ceilometer.conf.preceilosca
    fi
    # back up existing pipeline.yaml
    if [[ -e /etc/ceilometer/pipeline.yaml ]]; then
        cp /etc/ceilometer/pipeline.yaml /etc/ceilometer/pipeline.yaml.preceilosca
    fi

    for ceilosca_conf_file in $CEILOSCA_CONF_FILES
    do
        # source file and dest file names are separated with :
        source_file=`awk -F':' '{print $1}' <<< $ceilosca_conf_file`
        dest_file=`awk -F':' '{print $2}' <<< $ceilosca_conf_file`
        if [ -z $dest_file ]; then
            dest_file=$source_file
        fi
        cp $CEILOSCA_DIR/etc/ceilometer/$source_file /etc/ceilometer/$dest_file
    done

    # For reference, these ceilometer.conf options should be checked against
    # the current version and any updates made with each release.
    # https://docs.openstack.org/ceilometer/latest/configuration/

    # [database] removed after Pike
    # iniset $CEILOMETER_CONF database metering_connection monasca://$MONASCA_API_URL
    iniset $CEILOMETER_CONF notification workers $API_WORKERS
    # TODO: workload_partitioning deprecated in Rocky
    iniset $CEILOMETER_CONF notification workload_partitioning False
    # Disable, otherwise Ceilosca won't process and store event data
    # iniset $CEILOMETER_CONF notification disable_non_metric_meters False

    # Workaround: Client has a problem with the /identity auth url only in service_credentials
    auth_url=$(iniget $CEILOMETER_CONF service_credentials auth_url)
    #if [[ -n "$auth_url" ]]; then
    #    # Go direct to the port
    #    auth_url=${auth_url/%\/identity/:35357\/v3}
    #    iniset $CEILOMETER_CONF service_credentials auth_url ${auth_url}
    #fi

    # Add the [monasca] section and connection values
    iniset $CEILOMETER_CONF monasca service_auth_url ${auth_url}
    iniset $CEILOMETER_CONF monasca service_interface internalURL
    iniset $CEILOMETER_CONF monasca service_auth_type password

    # default monasca user for devstack (check monasca-api/devstack/plugin.sh)
    iniset $CEILOMETER_CONF monasca service_username mini-mon
    iniset $CEILOMETER_CONF monasca service_password password
    iniset $CEILOMETER_CONF monasca service_project_name mini-mon
    iniset $CEILOMETER_CONF monasca service_domain_name Default
    iniset $CEILOMETER_CONF monasca service_region_name RegionOne

    # leave the defaults for retry_on_failure, retry_interval,
    # enable_api_pagination, database_retry_interval, database_max_retries

    # Fill in Monasca URL in pipeline.yaml
    sed -i "s,monasca://INSERT-URL-HERE,monasca://${MONASCA_API_URL},g" /etc/ceilometer/pipeline.yaml
}

function preinstall_ceilosca {
    # create new directory --- removed in Rocky and Queens
    # cp -r $CEILOSCA_DIR/ceilosca/ceilometer/ceilosca_mapping $CEILOMETER_DIR/ceilometer/

    # overlay files into existing dirs
    for ceilosca_file in $CEILOSCA_FILES
    do
        # source file and dest file names are separated with :
        source_file=`awk -F':' '{print $1}' <<< $ceilosca_file`
        dest_file=`awk -F':' '{print $2}' <<< $ceilosca_file`
        if [ -z $dest_file ]; then
            dest_file=$source_file
        fi

        cp $CEILOSCA_DIR/ceilosca/$source_file $CEILOMETER_DIR/$dest_file
    done

    if ! grep -q "python-monascaclient" $CEILOMETER_DIR/requirements.txt; then
        sudo bash -c "echo python-monascaclient >> $CEILOMETER_DIR/requirements.txt"
    fi

}

# check for service enabled
if is_service_enabled ceilosca; then

    if [[ "$1" == "stack" && "$2" == "pre-install" ]]; then
        # Set up system services
        echo_summary "Configuring system services ceilosca"
        preinstall_ceilosca


    elif [[ "$1" == "stack" && "$2" == "install" ]]; then
        # Perform installation of service source
        echo_summary "Installing ceilosca"
        install_ceilosca

    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        # Configure after the other layer 1 and 2 services have been configured
        echo_summary "Configuring ceilosca"
        configure_ceilosca

    elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
        # Initialize and start the template service
        echo_summary "Initializing ceilosca"
        init_ceilosca
    fi

    if [[ "$1" == "unstack" ]]; then
        # Shut down template services
        # no-op
        :
    fi

    if [[ "$1" == "clean" ]]; then
        # Remove state and transient data
        # Remember clean.sh first calls unstack.sh
        # no-op
        :
    fi
fi
