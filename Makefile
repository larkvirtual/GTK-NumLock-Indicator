info:
	@echo 'Targets: info, install, uninstall'

install:
	ansible-playbook deploy-numlock-status.yml -t install

uninstall:
	ansible-playbook deploy-numlock-status.yml -t remove
