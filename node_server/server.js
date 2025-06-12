// Using Node js as backend for scrapping data

try{
    const request = require('request')
    console.log(request)
    request('https://www.sharesansar.com/', function (
  error,
  response,
  body
) {
  console.error('error:', error)
  console.log('body:', body)
})




}catch(e){
    console.log("Error in loading Request Module")
}

