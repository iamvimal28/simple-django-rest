# simple-django-rest
Integrating the chatbot model with Django REST API

# Steps to test: <br/>
1. Clone the repository <br/>
2. Navigate to ``chatbotapi`` directory <br/>
3. Run command ``python .\manage.py runserver localhost:8000`` <br/>
4. Test url ``POST http://localhost:8000/controller/handlerequest`` <br/>
5. Request Body: <br/>
    ```javascript
    {"msg":"Hi"}
    ```   
6. Response: <br/>
    ```javascript
    {"reply": "Hello, thanks for asking "}
    ```
