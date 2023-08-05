
Sends event if the yarn-cluster is empty/free to trigger other stuff (e.g. send you an email or start another application)

The HadoopYarnClusterChecker-Class checks your cluster if there is any application run on it. In case your cluster is free it fires an event.

# how it works:
* it's false positive: if there is any error like it can not connect to your yarn-rest-api it sends the event.
* algorithm:
  * receive data from: "/ws/v1/cluster/apps"-REST endpoint
  * are there applications with the state "running"?
    * Yes: Is this application excluded?
    * Yes: Are there more running applications?
      * No: send the event
      * Yes: sleep for the intervall & start with the first bulletin-point
# Excludes
* has to be a String
* excludes for state-attribute are forbidden!
* don't forget to escape the \"
* JSON-Notation:
  * Array
  * Key-Value-Object
  * Key: XML-Tag from the Yarn-Api
  * example: 
  ```json
  "[
  {\"name\":\"Zeppelin\"},
  {\"name\":\"Zeppelin1\"}
  ]"
  ```
    * meaning: all Applications with the Name "Zeppelin" and "Zeppelin1" will be excluded in case they're running
    * filtering:
      * for state-attribute is forbidden!
      * for multiple attributes like an AND should work:
        ```json
        [
         {
          "name":"Zeppelin", 
          "priority":0
          }
        ]
        ```

# How to use it:

```python
import hadoop-yarn-cluster-checker-lib

checker = HadoopYarnClusterChecker(server=args.server, path=args.path, intervall=args.intervall, log=args.log,
                                                               excludes=args.excludes)
checker.on_empty_cluster += event_empty
```

# Donations
[![paypal](https://www.paypalobjects.com/en_US/DK/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=EN22Z95HKGD74&source=url) 

# Cheatsheet for me
lore ipsem
## Twine
only works with: twine upload --repository-url https://test.pypi.org/legacy/ dist/*
