VERSION="1.0.0"
USER='guillain'

add(){
  echo "add: ${1}, comment: ${2}"
  git add -f "${1}"
  git commit -m "${2}" "${1}"
}

git pull
add README.md 'REDAME file'
add LICENSE 'LICENSE file'
add requirements.txt 'Software requirement'
add SoI4IoT.wsgi 'Apache WSGI configuration file'
add conf/settings.cfg.default 'Default config file to use as template'
add conf/apache.conf.default 'Default apache web server config file to use as template'
add conf/apache-secure.conf.default 'Default secure apache web server config file to use as template'
add conf/mysql.sql 'MySQL structure'
add test/test.wsgi 'Test file for Apache WSGI'
add SoI4IoT/__init__.py 'App init'
add SoI4IoT/static/image/loading.gif 'Animated gif'
add SoI4IoT/static/css/SoI4IoT.css 'CSS file of SoI4IoT'
add SoI4IoT/static/css/bootstrap.min.css 'CSS bootstrap'
add SoI4IoT/static/js/jquery-1.9.0.js 'jQuery'
add SoI4IoT/static/js/SoI4IoT.js 'jQuery of SoI4IoT'
add SoI4IoT/static/js/jquery.popupoverlay.js 'Popup mgt'
add SoI4IoT/static/__init__.py 'App Init file that contain web login mgt'
add SoI4IoT/static/py/__init__.py 'App init'
add SoI4IoT/static/py/SoI4IoT.py 'Main program'
add SoI4IoT/static/py/tools.py 'Tools library as DB connection, wEvent...'
add SoI4IoT/templates/view.html "View one element of the IoT DB"
add SoI4IoT/templates/list.html "List elements of the IoT DB"
add SoI4IoT/templates/flash.html "Flash message"
add SoI4IoT/templates/dashboard.html "Dashboard layout to display map"
add SoI4IoT/templates/index.html "Main layout"
add SoI4IoT/templates/new.html "User creation form"
add SoI4IoT/templates/login.html "Login form"
add run.dev 'TOOLS: bash script to run web server, for dev only'
add git.sh 'TOOLS: to comit easily the project to git'

git commit -m "prepare for ${VERSION}"
git push

