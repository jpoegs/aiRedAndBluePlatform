import httplib, errno

def main():

    host_default = '127.0.0.1'
    port_default = '4040'

    host = raw_input('Enter the server (no port) [' + host_default + ']: ')
    port = raw_input('Enter the port [' + port_default + ']: ')

    if not host.strip():
        host = host_default
    if not port.strip():
        port = port_default

    server = host + ':' + str(port)

    print 'Set connection URL to', server

    command = ['dummy']

    while command[0] != 'quit':
        command = raw_input('> ').split()
        while len(command) == 0:
            command = raw_input('> ').split()
        if command[0] == 'start':
            if len(command) == 2:
                startGame(server, {'game_id': command[1]})
            else:
                print 'Error: Need one argument (game id)'
        elif command[0] == 'join':
            if len(command) == 2:
                joinGame(server, {'game_id': command[1]})
            else:
                print 'Error: Need one argument (game id)'
        elif command[0] == 'delete':
            if len(command) == 2:
                deleteGame(server, {'game_id': command[1]})
            else:
                print 'Error: Need one argument (game id)'
        elif command[0] == 'quit':
            print 'Bye'
        else:
            usage()

def poll(server, method, url):
    try:
        conn = httplib.HTTPConnection(server)
        conn.request(method, url)
        response = conn.getresponse()
        response.read()
        conn.close()
        return response
    except httplib.InvalidURL, err:
        print 'Error: ', err.message # usually means invalid/nonnumeric port
    except IOError, err:
        if (errno.errorcode[err.errno] == 'ENOEXEC'):
            print 'Error: Cannot reach the given URL. It may be incorrect, or your internet may be down.'
        elif (errno.errorcode[err.errno] == 'ECONNREFUSED'):
            print 'Error: Connection refused. Your URL may be incorrect, or the server may be down.'
        else:
            print IOError, err
    except:
        return None

def startGame(server, details):
    S_GAME_STARTED = 201
    S_GAME_EXISTS = 409

    response = poll(server, 'POST', '/game/' + details['game_id'])

    if not response:
        return

    if response.status == S_GAME_STARTED:
        print 'Game with id "' + details['game_id'] + '" created'
    elif response.status == S_GAME_EXISTS:
        print 'Error: Game with id "' + details['game_id'] + '" already exists'

def joinGame(server, details):
    S_GAME_JOINED = 201 # will be 200 (spec doc definition)
    S_GAME_NOT_FOUND = 404
    S_GAME_FULL = 410 # not yet implemented on serverside

    response = poll(server, 'GET', '/game/' + details['game_id'] + '/') # TODO: suffix url with 'join/'

    if not response:
        return

    if response.status == S_GAME_JOINED:
        print 'Game with id "' + details['game_id'] + '" joined'
    elif response.status == S_GAME_NOT_FOUND:
        print 'Error: No game with id "' + details['game_id'] + '"'
    elif response.status == S_GAME_FULL:
        print 'Error: Game with id "' + details['game_id'] + '" already full'

def deleteGame(server, details):
    S_GAME_DELETED = 200
    S_GAME_NOT_FOUND = 404
    S_GAME_INCOMPLETE = 405 # not yet implemented

    response = poll(server, 'DELETE', '/game/' + details['game_id'])

    if not response:
        return

    if response.status == S_GAME_DELETED:
        print 'Game with id "' + details['game_id'] + '" deleted'
    elif response.status == S_GAME_NOT_FOUND:
        print 'Error: No game with id "' + details['game_id'] + '"'
    elif response.status == S_GAME_INCOMPLETE:
        print 'Error: Game with id "' + details['game_id'] + '" is not complete yet'

def usage():
    print 'Available commands:'
    print '-- start GAME_ID'
    print '-- join GAME_ID'
    print '-- delete GAME_ID'
    print '-- quit'

if __name__ == "__main__":
    main()
