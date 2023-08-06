# Deepcon-package
Python package for the DEEPCON contact prediction tool at https://github.com/ba-lab/DEEPCON

## How to install DEEPCON package?
```bash
pip3 install deepcon
```
## How to test DEEPCON package?
```bash
wget https://raw.githubusercontent.com/ba-lab/deepcon-package/master/deepcon/test/1a0tP0.aln
```
```bash
python3
```
```python
import deepcon
from deepcon import deepconcovariance
deepconcovariance.main("1a0tP0.aln","1a0tP0.rr")
```
To print the contact map as image, add the image name as the last parameter (optional)
```
deepconcovariance.main("1a0tP0.aln","1a0tP0.rr", "1a0tP0.png")
```
### Python package developed by:
Chase Richards<br/>
Email: CNRichards@gmail.com
