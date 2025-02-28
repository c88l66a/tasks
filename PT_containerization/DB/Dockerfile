FROM postgres:15

ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=qwe
ENV POSTGRES_DB=email_and_phone

COPY pg_hba.conf /etc/postgresql/pg_hba.conf
COPY postgresql.conf /etc/postgresql/postgresql.conf

COPY init.sql /docker-entrypoint-initdb.d/

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]