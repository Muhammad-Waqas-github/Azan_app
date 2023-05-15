import React, { useEffect, useState } from "react";
import "./PrayerData.css"; // Import the CSS file

function PrayerData() {
  const [prayers, setPrayers] = useState([]);

  // fetch("/api/update", {
  //   method: "POST",
  //   headers: {
  //     "Content-Type": "application/json",
  //   },
  //   body: JSON.stringify(updateData),
  // })

  useEffect(() => {
    fetch("/api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      // body: JSON.stringify(updateData),
    })
      .then((response) => response.json())
      .then((data) => setPrayers(data))
      .catch((error) => console.error(error));
  }, []);

  const handleAzanStatusToggle = (prayer) => {
    // Update the Azan Status of the prayer and send the update to the server
    const updatedPrayers = prayers.map((p) => {
      if (p[0] === prayer[0]) {
        return [p[0], p[1], prayer[2] === "on" ? "off" : "on", p[3]];
      }
      return p;
    });
    setPrayers(updatedPrayers);
    sendUpdateToServer(
      prayer[0],
      "azan_status",
      prayer[2] === "on" ? "off" : "on"
    );
  };

  const handleDuaStatusToggle = (prayer) => {
    // Update the Dua Status of the prayer and send the update to the server
    const updatedPrayers = prayers.map((p) => {
      if (p[0] === prayer[0]) {
        return [p[0], p[1], p[2], prayer[3] === "on" ? "off" : "on"];
      }
      return p;
    });
    setPrayers(updatedPrayers);
    sendUpdateToServer(
      prayer[0],
      "dua_status",
      prayer[3] === "on" ? "off" : "on"
    );
  };

  // const sendUpdateToServer = (prayer, field, value) => {
  //   // Send the update to the server using an API call
  //   const updateData = { prayer, field, value };
  //   // Make the API call to send the update data to the server
  //   fetch("/api/update", {
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json",
  //     },
  //     body: JSON.stringify(updateData),
  //   })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       // Handle the response if needed
  //       console.log("Update sent successfully:", data);
  //     })
  //     .catch((error) => {
  //       // Handle any error during the API call
  //       console.error("Error sending update:", error);
  //     });
  // };

  const sendUpdateToServer = (prayer, field, value) => {
    // Send the update to the server using an API call
    const updateData = { prayer, field, value };
    // Make the API call to send the update data to the server
    fetch("/api/update", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateData),
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response if needed
        console.log("Update sent successfully:", data);
        // Update the local state with the updated data received from the server
        setPrayers(data);
      })
      .catch((error) => {
        // Handle any error during the API call
        console.error("Error sending update:", error);
      });
  };

  return (
    <div>
      <h1>Azan Times</h1>
      <table>
        <thead>
          <tr>
            <th>Prayer</th>
            <th>Azan Time</th>
            <th>Azan Status</th>
            <th>Dua Status</th>
          </tr>
        </thead>
        <tbody>
          {prayers.map((prayer) => (
            <tr key={prayer[0]}>
              <td>{prayer[0]}</td>
              <td>{prayer[1]}</td>
              <td>
                <label>
                  <input
                    type="checkbox"
                    checked={prayer[2] === "on"}
                    onChange={() => handleAzanStatusToggle(prayer)}
                  />
                  {prayer[2]}
                </label>
              </td>
              <td>
                <label>
                  <input
                    type="checkbox"
                    checked={prayer[3] === "on"}
                    onChange={() => handleDuaStatusToggle(prayer)}
                  />
                  {prayer[3]}
                </label>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PrayerData;
