import React, { useState, useEffect } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from "@mui/material";
import "../App.css";
import AxiosInstance from "./AxiosInstance";
import ReactMarkdown from "react-markdown";

const Chat = () => {
  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState({
    city: "",
    days: "",
    visit_date: "",
    num_people: "",
    interests: "",
  });
  const [response, setResponse] = useState(null);
  const [calendarOpen, setCalendarOpen] = useState(false);

  const handleChange = (field) => (event) => {
    setFormData({ ...formData, [field]: event.target.value });
  };

  const handleNextStep = () => {
    if (step === 2) {
      setCalendarOpen(true);
    } else {
      setStep(step + 1);
    }
  };

  const handleCalendarClose = (date) => {
    setCalendarOpen(false);
    if (date) {
      setFormData({ ...formData, visit_date: date });
      setStep(step + 1);
    }
  };

  const handleSubmit = async () => {
    try {
      const response = await AxiosInstance.post(
        `generate-itinerary/`,
        formData
      );
      console.log(response.data);
      setResponse(response.data);
    } catch (error) {
      console.error("Error generating itinerary:", error);
    }
  };

  const initializeResponseAndStep = () => {
    setResponse({
      itinerary:
        "### Sample Itinerary\n- Day 1: Visit the museum\n- Day 2: Explore nature parks\n- Day 3: Enjoy local food tours.",
    });
    setStep(4);
  };

  const autoCreateAndSubmit = () => {setFormData({
    ...formData,
    city: "Mangalore",
    days: "3",
    visit_date: "18-12-24",
    num_people: "3",
    interests: "Food",
  });
    setStep(4);
  };

  // useEffect(() => { initializeResponseAndStep(); }, []);
  
  // useEffect(() => { autoCreateAndSubmit(); }, []);

  const renderStep = () => {
    switch (step) {
      case 0:
        return (
          <>
            <Typography>
              Welcome! Which city are you planning to visit?
            </Typography>
            <TextField
              label="City"
              variant="outlined"
              value={formData.city}
              onChange={handleChange("city")}
              className="chat-textbox"
            />
            <Button onClick={handleNextStep}>Next</Button>
          </>
        );
      case 1:
        return (
          <>
            <Typography>How many days will you be staying?</Typography>
            <TextField
              label="Days"
              type="number"
              variant="outlined"
              value={formData.days}
              onChange={handleChange("days")}
              className="chat-textbox"
            />
            <Button onClick={handleNextStep}>Next</Button>
          </>
        );
      case 2:
        return (
          <>
            <Typography>When will you start your trip?</Typography>
            <Button onClick={() => setCalendarOpen(true)}>Select Date</Button>
          </>
        );
      case 3:
        return (
          <>
            <Typography>How many people are traveling?</Typography>
            <TextField
              label="Number of People"
              type="number"
              variant="outlined"
              value={formData.num_people}
              onChange={handleChange("num_people")}
              className="chat-textbox"
            />
            <Button onClick={handleNextStep}>Next</Button>
          </>
        );
      case 4:
        return (
          <>
            <Typography>
              What are your interests? (e.g., museums, nature, food)
            </Typography>
            <TextField
              label="Interests"
              variant="outlined"
              value={formData.interests}
              onChange={handleChange("interests")}
              className="chat-textbox"
            />
            <Button onClick={handleSubmit}>Submit</Button>
          </>
        );
      default:
        return null;
    }
  };

  return (
    <Box className="chat-container" sx={{ padding: 2 }}>
      {response ? (
        <Box
          sx={{
            border: "1px solid #ddd",
            padding: 2,
            borderRadius: 2,
            backgroundColor: "#f9f9f9",
          }}
        >
          <Typography
            variant="h6"
            sx={{ fontWeight: "bold", color: "#2C3E50" }}
          >
            Your Itinerary:
          </Typography>

          {/* Itinerary content */}
          <Box sx={{ marginTop: 2 }}>
            {response.itinerary ? (
              <Box sx={{ lineHeight: 1.8, fontSize: "1rem", color: "#333" }}>
                <ReactMarkdown>
                  {response.itinerary.text ||
                    response.itinerary.content ||
                    response.itinerary ||
                    ""}
                </ReactMarkdown>
              </Box>
            ) : (
              <Typography sx={{ fontStyle: "italic", color: "#7f8c8d" }}>
                Itinerary details are loading...
              </Typography>
            )}
          </Box>
        </Box>
      ) : (
        renderStep()
      )}
      {/* Calendar Dialog */}
      <Dialog open={calendarOpen} onClose={() => handleCalendarClose()}>
        <DialogTitle>Select Visit Date</DialogTitle>
        <DialogContent>
          <TextField
            type="date"
            onChange={(e) => handleCalendarClose(e.target.value)}
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => handleCalendarClose()}>Cancel</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Chat;
