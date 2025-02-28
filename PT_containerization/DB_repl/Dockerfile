FROM postgres:15

USER postgres

#ps1 ето имя контейнера master
CMD ["bash", "-c", "rm -rf /var/lib/postgresql/data/* && chmod -R 700 /var/lib/postgresql/data && sleep 10 && PGPASSWORD='qwe' pg_basebackup -R -h ps1 -U repl_user -D /var/lib/postgresql/data && exec postgres"]