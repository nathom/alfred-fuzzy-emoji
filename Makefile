WORKFLOW_DIR=/Users/nathan/Library/Application Support/Alfred/Alfred.alfredpreferences/workflows/user.workflow.0D0AE669-4EB7-4837-8B91-0EBB5E737234

build:
	go build main.go data.go
	rm -f "$(WORKFLOW_DIR)/main"
	cp ./main "$(WORKFLOW_DIR)/main"
