import boto3


###########################################################################
# Region
###########################################################################
default_region = None

def set_default_region(region: str):
    global default_region
    default_region = region

def get_default_region():
    global default_region

    if default_region is None: 
        raise Exception("You must call set_default_region() before calling get_default_region()")

    return default_region

def list_regions():
    """
    Returns a list of valid regions in AWS.
    """
    pass


def list_azs():
    """
    Returns a list of all availability zones on AWs.
    """
    pass

###########################################################################
# AMIs
###########################################################################
def list_linux2_ami(region: str = None):
    """
    Returns a list of all AMIs available in the current default region.
    :param region: The region to list the AMIs from.  If None, uses default region

    :return: list of AMIs
    """
    pass

def get_image(id: str, region: str = None):
    """

    :param id: ID of image.
    :return:
    """
    pass

###########################################################################
# VPC
###########################################################################
default_vpcid = None

def set_default_vpcid(vpc_id: str):
    global default_vpcid
    default_vpcid = vpc_id

def get_default_vpcid():
    global default_vpcid

    if default_vpcid is None: 
        raise Exception("You must call set_default_vpcid() before calling get_default_vpcid()")

    return default_vpcid

def list_vpcs(filter_name: str = None, filter_value: str = None, filter_list: list = None):
    pass

list_vpcs(filter_name = 'Name', filter_value = 'dev-vpc')



def get_vpc(vpc_id: str):
    pass

###########################################################################
# Subnets
###########################################################################

def list_subnets(vpc_id: str = None, filter_name: str = None, filter_value: str = None, filter_list: list = None):
    pass

def get_subnet(subnet_id: str):
    pass

###########################################################################
# Internet Gateways & NATs
###########################################################################

def list_igws():
    pass


def list_nats():
    pass

def list_eips():
    pass

###########################################################################
# Route Tables
###########################################################################

def list_route_tables():
    pass

def get_route_table(rt_id: str ):
    pass


###########################################################################
# Security Groups
###########################################################################

def list_sgs():
    pass

def get_sg():
    pass

###########################################################################
# EC2 Instances
###########################################################################

def list_instances():
    pass

def get_instance():
    pass

###########################################################################
# Tags
###########################################################################
def get_tags(obj: dict):
    pass