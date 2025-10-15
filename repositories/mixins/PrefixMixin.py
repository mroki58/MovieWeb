cmd1 =  """
        MATCH (m:{element_name}) 
        WHERE m.{search_name} STARTS WITH $prefix
        RETURN m
        """

class PrefixMixin:
    def find_element_by_prefix(self, element_name, search_name, prefix):
        cmd = cmd1.format(element_name=element_name, search_name=search_name)
        with self.driver.session() as session:
            result = session.run(
                cmd,
                prefix=prefix
            )
            res = [record['m'] for record in result]
        return res