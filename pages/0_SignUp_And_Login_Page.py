import streamlit as st
from  streamlit_option_menu import option_menu
import time
from src.users_module import Users


user = Users()

                

page = option_menu(
        menu_title=None,
        options=["Login", "Sign Up","Forgot Password"],
        icons=["person-lock", "person-plus","arrow-clockwise"],
        default_index=0,
        orientation="horizontal"
)

if page == "Sign Up":
        username = st.text_input("Enter a username")
        email = st.text_input("Enter your email:")
        password = st.text_input("Enter your password:", type="password")
        if st.button("Submit"):
            result = user.signup_section(email, password, username)
            if result["success"]:
                st.success(result["message"])
                time.sleep(1)
            
            else:
                st.error(result["message"])

elif page == "Login":
        email = st.text_input("Enter your email:")
        password = st.text_input("Enter your password:", type="password")
        if st.button("Submit"):
            result = user.login_section(email, password)
            if result["success"]:
                st.success(result["message"])
                st.session_state['loggedIn'] = True
                st.balloons()
                time.sleep(3)
                
            else:
                st.error(result["message"])
elif page == "Forgot Password":
        st.write("Please write a mail to : productiveai23@gmail.com , with the Subject as: FORGOT PASSWORD")

        # email = st.text_input("Enter your email:",key="th_em_ip")

        # if st.button("Reset Password"):

        #     if email:

        #         # Call the forgot_password_page function and pass the email as a parameter
        #         # result = user.forgot_password_page(email)

        #         # # Display the result to the user
        #         # if result["success"]:
        #         #     st.success(result["message"])
        #         # else:
        #         #     st.error(result["message"])
        #     else:
        #         st.warning("Please enter your email before resetting the password.")

        #         # st.write("Please write a mail to : productiveai23@gmail.com , with the Subject as: FORGOT PASSWORD")

with st.sidebar:
    if st.session_state["loggedIn"] == True:
        if st.button("Logout"):
            st.success("Successfully logged out....")
            st.session_state['loggedIn'] = False
            time.sleep(1)
            st.rerun()
            