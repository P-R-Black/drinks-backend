const apiContainer = document.querySelector('.api_result_container')
const displayArea = document.querySelector('.displayArea')

let newDrinkName, newId, newSlug, newProfile, newServingGlass, newMixingDirection, newDrinkType;
let newBaseAlcohol, newIngredientName, newGarnish, newMustKnow;

let testList = []


const getMostPopularAPi = async  () => {
    const response = await fetch('http://127.0.0.1:8000/api/most-popular/')
    const drinks = await response.json()
    // console.log('drinks', drinks)

    // let testList = []
    drinks.map((dr) => testList.push(dr))
    let justOneDrink = testList
    // console.log('justOneDrink', justOneDrink)
    newId = justOneDrink.id
    newDrinkName = justOneDrink.drink_name
    newSlug = justOneDrink.slug
    newProfile =  justOneDrink.profile
    newBaseAlcohol = String(justOneDrink.base_alcohol)
    newIngredientName = String(justOneDrink.ingredient_name)
    newGarnish = String(justOneDrink.garnish)
    newServingGlass = justOneDrink.serving_glass
    newMixingDirection = justOneDrink.mixing_direction
    newDrinkType = justOneDrink.drink_type
    newMustKnow = justOneDrink.must_know_drink


}

getMostPopularAPi()


const submitButton = document.querySelector('.show_api');

const showApi = () => {

    console.log('submitButton', submitButton)
    submitButton.addEventListener('click', (e) => {
        e.preventDefault()
        console.log('button clicked')
        displayArea.classList.add('addBackgroundColor')
        testList.forEach((tl) => {

            const pre = document.createElement('pre')
            const dataCodes =  document.createElement('code')
            const titleCodes = document.createElement('code')
            const idBoxDiv = document.createElement('div')
            const openBrackets = document.createElement('code')
            const closedBrackets = document.createElement('code')
            const openBars = document.createElement('div')


            apiContainer.appendChild(pre)
            pre.appendChild(openBrackets).classList.add('openBrackets')
            openBars.innerHTML = '['
            openBrackets.innerHTML = "{"

            // id
            pre.appendChild(idBoxDiv).classList.add('idBox')
                idBoxDiv.appendChild(titleCodes).classList.add('apiNameTitle')
                titleCodes.innerHTML = '"id": '
                idBoxDiv.appendChild(dataCodes).classList.add("api_drink_name")
                dataCodes.innerHTML = tl.id


            const nameDataCodes =  document.createElement('code')
            const nameTitleCodes = document.createElement('code')
            const nameBoxDiv = document.createElement('div')

            pre.appendChild(nameBoxDiv).classList.add('idBox')
            nameBoxDiv.appendChild(nameTitleCodes).classList.add('apiNameTitle')
            nameTitleCodes.innerHTML = '"drink_name": '
            nameBoxDiv.appendChild(nameDataCodes).classList.add("api_drink_name")
            nameDataCodes.innerHTML = `"${tl.drink_name}"`

            // slug
            const slugDataCodes =  document.createElement('code')
            const slugTitleCodes = document.createElement('code')
            const slugBoxDiv = document.createElement('div')

            pre.appendChild(slugBoxDiv).classList.add('idBox')
            slugBoxDiv.appendChild(slugTitleCodes).classList.add('apiNameTitle')
            slugTitleCodes.innerHTML = '"slug": '
            slugBoxDiv.appendChild(slugDataCodes).classList.add("api_drink_name")
            slugDataCodes.innerHTML = `"${tl.slug}"`

            // profile
            const profileDataCodes =  document.createElement('code')
            const profileTitleCodes = document.createElement('code')
            const profileBoxDiv = document.createElement('div')

            pre.appendChild(profileBoxDiv).classList.add('idBox')
            profileBoxDiv.appendChild(profileTitleCodes).classList.add('apiNameTitle')
            profileTitleCodes.innerHTML = '"profile": '
            profileBoxDiv.appendChild(profileDataCodes).classList.add("api_drink_name")
            profileDataCodes.innerHTML = `"${tl.profile}"`

            // baseAlc
            const baseAlcDataCodes =  document.createElement('code')
            const baseAlcTitleCodes = document.createElement('code')
            const baseAlcBoxDiv = document.createElement('div')

            pre.appendChild(baseAlcBoxDiv).classList.add('idBox')
            baseAlcBoxDiv.appendChild(baseAlcTitleCodes).classList.add('apiNameTitle')
            baseAlcTitleCodes.innerHTML = '"base_alcohol": '
            baseAlcBoxDiv.appendChild(baseAlcDataCodes).classList.add("api_drink_name")
            baseAlcDataCodes.innerHTML = `["${String(tl.base_alcohol).replaceAll(',', ', ')}"]`;

            // Ingredients
            const ingredientDataCodes =  document.createElement('code')
            const ingredientTitleCodes = document.createElement('code')
            const ingredientBoxDiv = document.createElement('div')

            pre.appendChild(ingredientBoxDiv).classList.add('idBox')
            ingredientBoxDiv.appendChild(ingredientTitleCodes).classList.add('apiNameTitle')
            ingredientTitleCodes.innerHTML = '"ingredient_name": '
            ingredientBoxDiv.appendChild(ingredientDataCodes).classList.add("api_drink_name")
            let allIngredients = tl.ingredient_name;
             let newIngredientList = []
            for (let i = 0; i < allIngredients.length; i++){
                newIngredientList.push(`"${allIngredients[i]}"`)
            }
            ingredientDataCodes.innerHTML = `[${newIngredientList}]`

            // garnish
            const garnishDataCodes =  document.createElement('code')
            const garnishTitleCodes = document.createElement('code')
            const garnishBoxDiv = document.createElement('div')

            pre.appendChild(garnishBoxDiv).classList.add('idBox')
            garnishBoxDiv.appendChild(garnishTitleCodes).classList.add('apiNameTitle')
            garnishTitleCodes.innerHTML = '"garnish": '
            garnishBoxDiv.appendChild(garnishDataCodes).classList.add("api_drink_name")

            let allGarnish = tl.garnish;
             let newGarnishList = []
            for (let i = 0; i < allGarnish.length; i++){
                newGarnishList.push(`"${allGarnish[i]}"`)
            }

            garnishDataCodes.innerHTML = `[${newGarnishList}]`


            // serving_glass
            const servGlassDataCodes =  document.createElement('code')
            const servGlassTitleCodes = document.createElement('code')
            const servGlassBoxDiv = document.createElement('div')

            pre.appendChild(servGlassBoxDiv).classList.add('idBox')
            servGlassBoxDiv.appendChild(servGlassTitleCodes).classList.add('apiNameTitle')
            servGlassTitleCodes.innerHTML = '"serving_glass": '
            servGlassBoxDiv.appendChild(servGlassDataCodes).classList.add("api_drink_name")
            servGlassDataCodes.innerHTML = `"${tl.serving_glass}"`;

            // mixing_direction
            const mixingGlassDataCodes =  document.createElement('code')
            const mixingGlassTitleCodes = document.createElement('code')
            const mixingGlassBoxDiv = document.createElement('div')

            pre.appendChild(mixingGlassBoxDiv).classList.add('idBox')
            mixingGlassBoxDiv.appendChild(mixingGlassTitleCodes).classList.add('apiNameTitle')
            mixingGlassTitleCodes.innerHTML = '"mixing_direction": '
            mixingGlassBoxDiv.appendChild(mixingGlassDataCodes).classList.add(`${"api_mix_name"}`)
            mixingGlassDataCodes.innerHTML = `"${tl.mixing_direction}"`;

            // drink type
            const drinkTypeDataCodes =  document.createElement('code')
            const drinkTypeTitleCodes = document.createElement('code')
            const drinkTypeBoxDiv = document.createElement('div')

            pre.appendChild(drinkTypeBoxDiv).classList.add('idBox')
            drinkTypeBoxDiv.appendChild(drinkTypeTitleCodes).classList.add('apiNameTitle')
            drinkTypeTitleCodes.innerHTML = '"drink_type": '
            drinkTypeBoxDiv.appendChild(drinkTypeDataCodes).classList.add("api_drink_name")
            drinkTypeDataCodes.innerHTML = `"${tl.drink_type}"`;

            // must knows
            const mustKnowsDataCodes =  document.createElement('code')
            const mustKnowsTitleCodes = document.createElement('code')
            const mustKnowsBoxDiv = document.createElement('div')

            pre.appendChild(mustKnowsBoxDiv).classList.add('idBox')
            mustKnowsBoxDiv.appendChild(mustKnowsTitleCodes).classList.add('apiNameTitle')
            mustKnowsTitleCodes.innerHTML = '"must_know_drink": '
            mustKnowsBoxDiv.appendChild(mustKnowsDataCodes).classList.add("api_drink_name")
            mustKnowsDataCodes.innerHTML = tl.must_know_drink;

            pre.appendChild(closedBrackets).classList.add('closedBrackets')
            closedBrackets.innerHTML = '},'
        })


    })
}

showApi()

