export POETRY_ENABLED := 1

SHELL=bash

fix:
	@printf "$(YELLOW)flake8$(COFF) will $(RED)not be executed$(COFF) in this task.\n"
	@printf " ----> Run '$(YELLOW)make check$(COFF)' to see flake8 results.\n"
	@printf " >>> $(CYAN)Running isort$(COFF)\n"
	isort forum_system_api tests
	@printf " >>> $(GREEN)isort done$(COFF)\n"
	@printf "$(CYAN)Auto-formatting with black$(COFF)\n"
	black forum_system_api tests
	@printf " >>> $(GREEN)black done$(COFF)\n"
	@printf "Generating $(CYAN)licenses.md$(COFF) file\n"
