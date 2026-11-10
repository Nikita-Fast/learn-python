

class ArgSpec:
    pass


class ScpiNode:
    children = []
    keyword = ""
    arg_spec = ""

    def match(self, cmd_keywords: list[str]):
        if len(cmd_keywords) == 0:
            return self

        target_keyword = cmd_keywords[0]
        for child in self.children:
            if child.keyword.upper() == target_keyword.upper():
                return child.match(cmd_keywords[1:])

        return None


if __name__ == '__main__':
    # SOURCE:VOLTAGE
    # SOURCE:CURRENT
    # *IDN?

    root = ScpiNode()

    node_source = ScpiNode()
    node_source.keyword = "SOURce"
    root.children.append(node_source)

    node_volt = ScpiNode()
    node_volt.keyword = "VOLTage"
    node_curr = ScpiNode()
    node_curr.keyword = "CURRent"
    node_source.children.extend([node_volt, node_curr])

    node_idn = ScpiNode()
    node_idn.keyword = "*IDN?"
    root.children.append(node_idn)

    # m = root.match(["SOURCE", "VOLTAGE"])
    m = root.match(["*idn?"])
    print(m.keyword if m is not None else m)