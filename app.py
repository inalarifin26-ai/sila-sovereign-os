        with st.chat_message("assistant"):
            # Pakai cara paling simpel, biarkan sistem yang atur jalurnya sendiri
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
