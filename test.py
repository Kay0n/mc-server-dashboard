import mcinfo

requester = mcinfo.MCInfo()

servers = ['refract.online', ' alt.refract.online', ' mini.refract.online', ' spin.refract.online', ' mv.refract.online']

print(requester.get_sorted_servers(servers))