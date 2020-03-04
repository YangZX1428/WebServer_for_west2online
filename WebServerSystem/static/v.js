const v1 = new Vue({
    el:'#content',
    data(){
        return {
                name:'aaaa',
                age:0,
                show:false,
                items:[],
                };

    },

    methods:{
        Getmore(){
            axios.get("http://127.0.0.1:5000/get_item/all").then(res => {
                this.name = "bbb";
                this.age = "123";
                this.show = !this.show;
                console.log(res.data.data[0]);
                this.items = res.data.data[0];

            })
        },
        Getname(){
            return "name = "+this.name;
        },
        Getage(){
            return "age = "+this.age;
        },

    }
})