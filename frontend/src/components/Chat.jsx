import React from 'react';
import { Box, TextField } from '@mui/material';
import '../App.css';

const Chat = () => {
    return (
        <Box className="chat-container">
            <TextField 
                label="Type something" 
                variant="outlined" 
                className="chat-textbox"
            />
        </Box>
    );
}

export default Chat;
