# takeoverdomain
Takeoverdomain is a Subdomain Takeover tool written in Python

*How To Use:

Usage: takeoverdomain.py [OPTIONS]

	-k --keyword		Set keyword (e.g: google)
	-d --domain		Set domain (e.g: google.com)
	-D --domain-list	Scan multiple targets in a text file
	-p --set-proxy		Use a proxy to connect to the target URL
	-o --set-output		Use this setting for save a file
	-t --set-timeout	Set a request timeout. Default value is 2 seconds

Example:
	python takeoverdomain.py --domain google.com
  python takeoverdomain.py -D domains.txt
  
Ref:
https://github.com/EdOverflow/can-i-take-over-xyz
