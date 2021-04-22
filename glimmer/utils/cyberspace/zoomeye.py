import zoomeye.sdk as zoomeye

from glimmer.libs.core.exceptions import ParserExceptions


class ZoomeyeClient:
    def __init__(self, key):
        self.key = key
        self.api = zoomeye.ZoomEye(api_key=key)

    def query(self, query_str, max_page=1, resource="host", fields="", facets=None):
        """
        support resource:
            web, host
        support fields:
            resource == web
                app headers keywords title ip site city country
            resource == host
                app version device ip port hostname city country asn banner
        support facets:
            app, device, service, os, port, country, city
        """
        if resource not in ["host", "web"]:
            raise ParserExceptions.CyberSpace.APIError("resource must be host / web")

        data = self.api.multi_page_search(
            query_str, max_page, resource, facets)
        self.data = data
        if facets:
            return self.get_facet()
        elif fields == "":
            return data
        else:
            return self.get_fields(fields)

    def get_data(self):
        """
        use after query, get all data.
        """
        return self.data

    def get_fields(self, fields):
        """
        use after query, get fields from data.
        """
        return self.api.dork_filter(fields)

    def get_facet(self):
        """
        use after query, get data facet if you had set facets parameter in query.
        """
        return self.api.get_facet()

    def show_site_ip(self, data):
        """
        use after query, get domain and ip from all data.
        """
        return zoomeye.show_site_ip(self.data)

    def show_ip_port(self, data):
        """
        use after query, get ip and port from all data.
        """
        zoomeye.show_ip_port(self.data)
