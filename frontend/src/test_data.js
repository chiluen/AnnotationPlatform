/*
This file is for testing frontend application
*/


// login data
var login_data = {
    user: "leo",
    password: "leo"
};

// user data
var user_data = {
    name: "leo",
    numberOfUpload: 30,
    numberOfReview: 10,
    reviewRank: 4
}

var state_sample = {
    labels: ["Percentage"],
    datasets: [
      {
        label: 'Finish',
        backgroundColor: "#FEC5BB", 
        borderColor: 'rgba(0,0,0,1)',
        borderWidth: 2,
        data: [10]
      },
      {
        label: 'Unfinish',
        backgroundColor: "#FAE1DD", 
        borderColor: 'rgba(0,0,0,1)',
        borderWidth: 2,
        data: [90]
      }
    ]
}

var datasets_sample = [
    {
      data: [5,30,10,2,80,100],
      backgroundColor: ["#FEC5BB", "#FAE1DD", "#E8E8E4", "#ECE4DB", "#FFE5D9"]
    }
]


var db_sample = [5.6, "56%", 3001] //這個不符合Json樣式，在改API時要注意


var list_example = [
    {
    data: "kasjfklsdjflkasdjflkasdjdlkfjasdklfjdjfkasjdfklasjdflkasjklfdskjflsadjfldfjalkdjflasdfjksfjlakdjflasdjfalskfjadlskjfkl",
    status: "P",
    rank: 5
    },
    {
        data: "sfkldasdjflkajflaskdjflsajfldksjfldkjfladsdfjladskfjlasdkfjlasdkfjals",
        status: "P",
        rank: 5
    },
    {
        data: "sfkldasdjflkajflaskdjflsajfldksjfldkjfladsdfjladskfjlasdkfjlasdkfjals",
        status: "P",
        rank: 3
    },
    {
        data: "sfkldasdjflkajflaskdjflsajfldksjfldkjfladsdfjladskfjlasdkfjlasdkfjals",
        status: "P",
        rank: 5
    },
    {
        data: "sfkldasdjflkajflaskdjflsajfldksjfldkjfladsdfjladskfjlasdkfjlasdkfjals",
        status: "P",
        rank: 1
    },
    {
        data: "sfkldasdjflkajflaskdjflsajfldksjfldkjfladsdfjladskfjlasdkfjlasdkfjals",
        status: "N",
        rank: 5
    },
    {
        data: "sfkldasdjflkajflaskdjflsajfldksjfldkjfladsdfjladskfjlasdkfjlasdkfjals",
        status: "X",
        rank: 5
    },
    {
        data: "sfkldasdjflkajflaskdjflsajfldksjfldkjfladsdfjladskfjlasdkfjlasdkfjals",
        status: "X",
        rank: 4
    },
    {
        data: "sfkldasdjflkajflaskdjflsajfldksjfldkjfladsdfjladskfjlasdkfjlasdkfjals",
        status: "P",
        rank: 5
    },
    {
        data: "sfkldasdjflkajflaskdjflsajfldksjfldkjfladsdfjladskfjlasdkfjlasdkfjals",
        status: "P",
        rank: 5
    },
    {
        data: "sfkldasdjflkajflaskdjflsajfldksjfldkjfladsdfjladskfjlasdkfjlasdkfjals",
        status: "X",
        rank: 4
    },
    {
        data: "sfkldasdjflkajflaskdjflsajfldksjfldkjfladsdfjladskfjlasdkfjlasdkfjals",
        status: "X",
        rank: 4
    },
    {
        data: "sfkldasdjflkajflaskdjflsajfldksjfldkjfladsdfjladskfjlasdkfjlasdkfjals",
        status: "X",
        rank: 4
    },
    {
        data: "eee",
        status: "X",
        rank: 2
    },
]

var annotation_example = [
    {
        remain: 30,
        data: "The Interview was neither that funny nor that witty The Interview was neither that funny nor that witty "
    },
    {
        remain: 15,
        data: "Neither that funny nor that witty The Interview was neither that funny nor that witty "
    },
    {
        remain: 2,
        data: "Funny nor that witty Funny nor that witty Funny nor that witty Funny nor that witty Funny nor that witty "
    }
]

var review_example = [
    {
        remain: 30,
        data: "The Interview was neither that funny nor that witty The Interview was neither that funny nor that witty ",
        classification: "Positive"
    },
    {
        remain: 15,
        data: "Neither that funny nor that witty The Interview was neither that funny nor that witty ",
        classification: "Negative"
    },
    {
        remain: 2,
        data: "Funny nor that witty Funny nor that witty Funny nor that witty Funny nor that witty Funny nor that witty ",
        classification: "Neutral"
    }
]








export { login_data,user_data, state_sample, datasets_sample, db_sample, list_example, annotation_example, review_example };