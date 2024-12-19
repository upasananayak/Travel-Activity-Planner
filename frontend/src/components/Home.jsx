import React from "react";
import { Box, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import "../App.css";

const Home = () => {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate(`/login`);
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
          onClick={handleButtonClick}
        >
          Login
        </Button>
        {/* <Button
          variant="contained"
          color="primary"
          sx={{
            backgroundColor: "#1c5996",
            "&:hover": { backgroundColor: "#144272" },
          }}
          onClick={handleButtonClick}
        >
          View Your Trips
        </Button> */}
      </Box>
    </Box>
  );
};

export default Home;
