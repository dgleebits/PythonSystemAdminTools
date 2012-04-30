def IPsearch(data):
    for line in data:
        if "Failed password for root from" in line:
            find_match = ip.search(line)
            IPaddress = find_match.group()
            if len(IPaddress) > 6:
                Ip = IPaddress.split(" ")[0]
                IpHitListing[Ip] = IpHitListing.get(Ip, 0) + 1
    return IpHitListing