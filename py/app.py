from flask import Flask, request
import json
from create_dummies import generate_users, generate_events

app = Flask(__name__)

@app.route('/notifications', methods=['GET', 'DELETE'])
def get_notification():
    if request.method == 'GET':
        with open('notification_queue.json', 'r') as f:
            obj = json.load(f)
            f.close()
        if len(obj['notifications']) > 0:
            return obj['notifications'][0]
        else:
            generate_events(5)
            return '''
            No notifications in queue.
            Generated 5 new events.
            Please perform a new GET request in order to retrieve the next notifications.
            '''

    elif request.method == 'DELETE':
        with open('notification_queue.json', 'r') as f:
            obj = json.load(f)
            f.close()
        obj['notifications'].pop(0)
        
        with open('notification_queue.json', 'w') as f:
            f.write(json.dumps(obj, indent=4))
            f.close()
        
        return '''
        \nNotification successfully removed.
        '''


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)