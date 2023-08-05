# Installation

1. Make sure your computer has the commercial engine installed. This can be achieved by installing either the [OpenALPR Agent](http://doc.openalpr.com/on_premises.html#installation) or the [Commercial SDK](http://doc.openalpr.com/sdk.html#installation). This ensures that the C code bound to this Python package is available on your system.

2. IMPORTANT: you cannot use this package without a product license. If you need an evaluation license, please request one [here](https://license.openalpr.com/evalrequest/).

3. Install this Python binding: `pip install openalpr`

# Example

Download and image of a car with the license plate visible, save to your computer, and run the following code:

```python
import json
from openalpr import Alpr

alpr = Alpr("us", "/path/to/openalpr.conf", "/path/to/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)
results = alpr.recognize_file("/path/to/image.jpg")
print(json.dumps(results, indent=4))
alpr.unload()
```

On Linux systems, the default paths for files required to instantiate the Alpr class are 

* `/etc/openalpr/openalpr.conf` 
* `/usr/share/openalpr/runtime_data`

And on Windows systems

* `C:\OpenALPR\Agent\etc\openalpr\openalpr.conf` 
* `C:\OpenALPR\Agent\usr\share\openalpr\runtime_data`

