def get_url_by_ip_port_domain(ip, port, domain=""):
    protocol = "http"
    port = str(port)
    if str(port) in ["443", "8443"]:
        protocol = "https"
    if domain:
        return f"{protocol}://{domain}/"
    else:
        return f"{protocol}://{ip}:{port}/"
