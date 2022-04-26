FROM python:3.8
EXPOSE 8501
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["streamlit", "run"]
CMD ["kpis_streamlit.py"]
