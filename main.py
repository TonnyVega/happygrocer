from website import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

# this was my first attempt with blue prints and slight functioning inventory app, with a rough template.
# with this I can now add a resource management system for a small or industrial grocery store.
# I will continue updating. 
# key notes. *admin page. * user page with profile updates. * user orders and admin dispatches. 
