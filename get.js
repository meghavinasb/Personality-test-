async function getStaffData(staffId) {
  try {
    const response = await fetch(
      `https://yk2109.pythonanywhere.com/get_staff_data/${staffId}`
    );
    if (response.ok) {
      const data = await response.json();
      console.log("Staff positive quote:\n", data.low_quote, "\n");
      console.log("Staff negative quote:\n", data.top_quote, "\n");
      // Process the retrieved data
    } else {
      console.error(
        "Error fetching data:",
        response.status,
        response.statusText
      );
    }
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

getStaffData(135);
