with netns.NetNS(nsname=args.ns):
    chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "PREROUTING")
    rule = iptc.Rule()
    rule.protocol ="tcp"
    match = iptc.Match(rule, "tcp")
    match.dport = args.outport
    target = rule.create_target("DNAT")
    target.to_destination = "{}:{}".format(args.server,args.inport)
    rule.add_match(match)
    rule.target = target
    chain.insert_rule(rule)

with netns.NetNS(nsname=args.ns):
    chain = iptc.Chain(iptc.Table(iptc.Table.NAT),"POSTROUTING")
    rule = iptc.Rule()
    rule.protocol ="tcp"
    rule.dst = args.server
    match = iptc.Match(rule , "tcp")
    match.dport = args.inport
    rule.add_match(match)
    rule.target = iptc.Target(rule, "MASQUERADE")
    chain.insert_rule(rule)
