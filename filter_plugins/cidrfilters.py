def netcidr_to_mask(s):
    return cidr_to_mask(cidr_from_netcidr(s))

def cidr_to_mask(s):
    mask_int = 2 ** 32 - 2 ** (32 - int(s))
    return ".".join(map(lambda n: str(mask_int >> n & 0xFF), [24, 16, 8, 0]))

def net_from_netcidr(s):
    return s.split("/")[0]

def cidr_from_netcidr(s):
    return s.split("/")[1]

class FilterModule(object):
    """ Utility filters for cidr """
    def filters(self):
        return {
            "net_from_netcidr": net_from_netcidr,
            "cidr_from_netcidr": cidr_from_netcidr,
            "netcidr_to_mask": netcidr_to_mask,
            "cidr_to_mask": cidr_to_mask
        }
