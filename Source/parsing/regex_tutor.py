import re


# scpi_cmd_pattern = r"(?P<header>SOURCE:FREQ) (?P<args>[\w.]+)"
# p = re.compile(scpi_cmd_pattern)
#
# m = p.match("SOURCE:FREQ 11.15GHZ")
# print(m.groups())
# print(m.groupdict())

# p = re.compile('x*')
# print(p.sub('-', 'abxd'))

# OUTPut[:STATe] <bool>
# <bool> -> 0|OFF|1|ON
# [OUTPut:]PROTection:CLEar
# [SOURce:]CURRent <NRf+>
# <NRf+> ->
# SOURce:VOLTage

# MEASure[:SCALar]:CURRent[:DC]?
# STATus:QUEStionable:CONDition?

# MEAS -> SCAL -> CURR -> DC

# regex for numbers 0..255
p = re.compile(r"[1-2]\d{2}|\d{2}|\d{1}")
m = p.match("256")
print(m)


