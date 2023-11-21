from src import create_app
from src.models import Member
from src.extensions import db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "Member": Member
    }
    
if __name__ == '__main__':
    app.run()
