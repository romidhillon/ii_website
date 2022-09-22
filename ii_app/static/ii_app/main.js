function Calculate() {
    const CP = document.querySelector(".cost__price").value;
    const SP = document.querySelector(".selling__price").value;
    
    const profit__loss = document.querySelector(".profit__loss");
    const percentage = document.querySelector(".profit__loss__percentage");
    const nothing = document.querySelector(".nothing");
    
    profit__loss.innerHTML = "";
    percentage.innerHTML = "";
    nothing.innerHTML = "";
    
    if (SP > CP) {
      const profit = SP - CP;
      const profit_percent = ((profit / CP) * 100).toFixed(2);
    
      profit__loss.innerHTML = "Profit : " + profit;
      percentage.innerHTML = "Profit Percentage : " + profit_percent;
    }
    if (SP < CP) {
      const loss = CP - SP;
      const loss_percent = ((loss / CP) * 100).toFixed(2);
    
      profit__loss.innerHTML = "Loss : " + loss;
      percentage.innerHTML = "Loss Percentage : " + loss_percent;
    }
    if (SP == CP) {
      nothing.innerHTML = "No Profit No Loss";
    }
  };