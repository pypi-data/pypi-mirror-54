# DMARC (Domain-based Message Authentication, Reporting & Conformance)

This module allows an application to parse and evaluate email authentication policy, to application supplied TXT RR, SPF and DKIM results.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dmarc.

```bash
pip install dmarc
```

## Usage

```python
>>> import dmarc

# represent verified SPF and DKIM status
>>> aspf = dmarc.SPF(domain='news.example.com', result=dmarc.SPF_PASS)

>>> adkim = dmarc.DKIM(domain='example.com', result=dmarc.DKIM_PASS)

>>> d = dmarc.DMARC()

# parse policy TXT RR
>>> p = d.parse_record(record='v=DMARC1; p=reject;', domain='example.com')

# evaluate policy
>>> r = d.get_result(p, spf=aspf, dkim=adkim)

# check result
>>> r.result == dmarc.POLICY_PASS
True

# check disposition
>>> r.disposition == dmarc.POLICY_DIS_NONE
True
```

## License
[MIT](https://choosealicense.com/licenses/mit/)