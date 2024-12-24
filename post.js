async function addPersonalityTestData(data) {
  try {
    const response = await fetch(
      "https://yk2109.pythonanywhere.com/personalitytest",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    );

    if (response.ok) {
      const responseData = await response.json();
      console.log("Data added successfully:", responseData);
      // Handle success (e.g., update UI)
    } else {
      console.error("Error adding data:", response.status, response.statusText);
    }
  } catch (error) {
    console.error("Error adding data:", error);
  }
}

const newData = {
  staff_id: "135",
  staff_name: "Ms. Jayapriya",
  response_1: "Motivational",
  response_2: "Patience",
  response_3: "Dedication",
};

addPersonalityTestData(newData);
