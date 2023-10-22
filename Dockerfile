FROM python:3.10

# working dictory on container
WORKDIR /code

#RUN apt-get update && apt-get install -y sudo
#RUN groupadd -r macro && useradd -r -g macro macro
#RUN addgroup --system macroferia && adduser --system --ingroup macroferia macro

# copy python requirements
COPY ./requirements.txt /app/requirements.txt

# install python requirements
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy project
COPY ./ /app/
#RUN chown -R macro:macroferia /app
#USER macro

EXPOSE 80

# run a the app in a single thread?
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
