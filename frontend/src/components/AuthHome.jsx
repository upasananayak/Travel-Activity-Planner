import React from "react";
import { Box, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import "../App.css";

const AuthHome = () => {
  const navigate = useNavigate();

  const handleChatButtonClick = () => {
    navigate('/chat');
  };
  const handleTripButtonClick = () => {
    navigate('/trip');
  };

  return (
    <Box className="myBackground">
      <Box
        className="centeredContent"
        sx={{ display: "flex", flexDirection: "column", gap: 2 }}
      >
        <Button
          variant="contained"
          color="primary"
          sx={{
            backgroundColor: "#1c5996",
            "&:hover": { backgroundColor: "#144272" },
          }}
          onClick={handleChatButtonClick}
        >
          Build a Trip
        </Button>
        <Button
          variant="contained"
          color="primary"
          sx={{
            backgroundColor: "#1c5996",
            "&:hover": { backgroundColor: "#144272" },
          }}
          onClick={handleTripButtonClick}
        >
          View Your Trips
        </Button>
      </Box>
    </Box>
  );
};

export default AuthHome;
