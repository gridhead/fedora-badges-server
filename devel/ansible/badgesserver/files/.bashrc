# .bashrc

alias badges-server-status="sudo systemctl status badges_server.service"
alias badges-server-start="sudo systemctl start badges_server.service && badges-server-status"
alias badges-server-logs="sudo journalctl -u badges_server.service"
alias badges-server-restart="sudo systemctl restart badges_server.service && badges-server-status"
alias badges-server-stop="sudo systemctl stop badges_server.service && badges-server-status"
