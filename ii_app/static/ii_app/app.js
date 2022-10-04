
// function to calculate the margin 
function CalculateMargin() {
    const costPerDay = document.querySelector(".cost_per_day").value
    const fullRate = document.querySelector(".full_rate").value

    const postCommissionRate = fullRate * 0.85
    const margin = postCommissionRate - costPerDay
    const marginPercentage = (margin / postCommissionRate) * 100

    const postCommissionRateElement = document.querySelector(".post_commission_rate")
    const marginElement = document.querySelector(".margin")
    const marginPercentageElement = document.querySelector(".margin_percentage")

    postCommissionRateElement.innerText = `Post Commission: ${postCommissionRate.toFixed(2)}`
    marginElement.innerText = "Margin : " + margin.toFixed(2)
    marginPercentageElement.innerText = "Margin Percentage : " + marginPercentage.toFixed(2)
}

function margin () {

    const chargeRate = document.querySelector(".rate").value
    const cone = document.querySelector(".cone").value
    

}

// function to calculate the life to date value
