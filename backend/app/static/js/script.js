document.addEventListener("DOMContentLoaded", () => {
  const scanButton = document.getElementById("scanButton");
  const domainInput = document.getElementById("domainInput");
  const loadingIndicator = document.getElementById("loading");
  const resultsDiv = document.getElementById("results");

  // Function to update UI states
  function updateUI(isLoading) {
    scanButton.disabled = isLoading;
    loadingIndicator.style.display = isLoading ? "block" : "none";
  }

  // Function to display results in a table
  function displayResults(data) {
    resultsDiv.innerHTML = `
      <table class="table table-hover table-bordered shadow-sm">
         <thead class="bg-primary text-white">
          <tr><th>Field</th><th>Value</th></tr>
        </thead>
        <tbody>
          <tr><td>Domain</td><td>${data?.domain || "N/A"}</td></tr>
          <tr><td>Related IPs</td><td>${Array.isArray(data?.related_ips) ? data.related_ips.join(", ") : "N/A"}</td></tr>
          <tr><td>Webpage Title</td><td>${data?.webpage_title || "N/A"}</td></tr>
          <tr><td>Status Code</td><td>${data?.status_code || "N/A"}</td></tr>
          <tr><td>Webserver</td><td>${data?.webserver || "N/A"}</td></tr>
          <tr><td>Technologies</td><td>${Array.isArray(data?.technologies) ? data.technologies.join(", ") : "N/A"}</td></tr>
          <tr><td>CNAMEs</td><td>${Array.isArray(data?.cnames) ? data.cnames.join(", ") : "N/A"}</td></tr>
        </tbody>
      </table>
    `;
  }

  async function handleScan() {
    const domain = domainInput.value.trim();
    resultsDiv.innerHTML = ""; // Clear previous results

    if (!domain) {
      resultsDiv.innerHTML = '<p class="text-danger">Please enter a domain name.</p>';
      return;
    }

    updateUI(true); // Show loading state

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 seconds timeout

    try {
      const response = await fetch(`/api/scan?domain=${encodeURIComponent(domain)}`, {
        signal: controller.signal,
      });
      clearTimeout(timeoutId);

      if (!response.ok) {
        let errorDetail = '';
        try {
          const errorData = await response.json();
          errorDetail = errorData.detail ? ` - ${errorData.detail}` : "";
        } catch (e) {
          console.error("Error parsing error response:", e);
        }
        updateUI(false);
        resultsDiv.innerHTML = `<p class="text-danger">Server error: ${response.statusText}${errorDetail}</p>`;
        console.error(`Server error: ${response.statusText}${errorDetail}`);
        return;
      }

      const data = await response.json();
      updateUI(false);
      displayResults(data);
    } catch (error) {
      updateUI(false);
      // Handle timeout error separately
      if (error.name === "AbortError") {
        resultsDiv.innerHTML = `<p class="text-danger">Request timed out. Please try again.</p>`;
      } else {
        console.error("Fetch error:", error);
        resultsDiv.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
      }
    }
  }

  // Attach event listeners with proper promise handling
  scanButton.addEventListener("click", async () => await handleScan());
  domainInput.addEventListener("keypress", async (event) => {
    if (event.key === "Enter") await handleScan();
  });
});
