
.PHONY: default
default:
	@echo "available commands:"
	@echo "  dist"

.PHONY: dist
dist:
	nr pybundle --dist --entry @houdini-manage-gui=houdini_manage.gui:main \
			--entry houdini-manage=houdini_manage.gui:main
