
import { createRouter, createWebHistory } from "vue-router";
// const recom = {
// 	template: `<router-view></router-view>`
// }
const refresh =() =>import("../components/RefreshPage.vue")
const main = () => import("../views/main")
const WrongQuestionEnter =()=>import("../components/WrongQuestionEnter.vue")
const WrongQuestion = () => import("../views/WrongQuestion.vue")
const QuestionPage = ()=>import("../components/QuestionPage.vue")
const StudentQuestionList =()=>import("../components/StudentQuestionList.vue")

const CollectQuestionEnter =()=>import("../components/CollectQuestionEnter.vue")
const CollectQuestion = () => import("../views/CollectQuestion.vue")
const CollectQuestionPage =()=>import("../components/CollectQuestionPage.vue")
const StudentQuestionPage=()=>import("../components/StudentQuestionPage.vue") 
const StudentQuestionEnter=()=>import("../components/StudentQuestionEnter.vue")

const ClassListEnter =()=>import("../components/ClassListEnter.vue")
const ClassList = () => import("../views/ClassList.vue")
const CalssInfo = () => import("../components/ClassInfo.vue")

const ClassStudentEnter =()=>import("../components/ClassStudentEnter.vue")
const ClassStudent =()=>import("../views/ClassStudent.vue")
const StudentInfo =()=>import("../components/StudentInfo.vue")

const ApplyListEnter =()=>import("../components/ApplyListEnter.vue")
const ApplyList = ()=>import("../views/ApplyList.vue")

const AddList =()=>import("../views/AddList.vue")


const routes = [
    {
        path: "/", redirect: "/main"
    },
    {
        path:"/refresh",name:'refresh',component:refresh
    },
    {
        path: '/main', name: "main", component: main
    },
    {
        path: '/wrongquestion', name: "wrongquestion", component: WrongQuestionEnter,children:[
            { path: 'question/:pid', component: QuestionPage },
            {path:'',component:WrongQuestion},
        ]
    },
    {
        path: '/collectquestion', name: "collectquestion", component: CollectQuestionEnter,children:[
            { path: 'question/:pid', component: CollectQuestionPage },
            {path:'',component:CollectQuestion},
        ]
    },
    {
        path: '/classlist',component:ClassListEnter, children: [
            { path: 'classinfo/:cid', component: CalssInfo },
            {path:'',component:ClassList},
            {path:'class/:cid/:cname',component:ClassStudentEnter,children:[
                {path:'',component:ClassStudent},
                {path:'studentinfo/:sid',component:StudentInfo},
                {path:'studentwrongquestion/:sid',component:StudentQuestionEnter,children:[
                    {path:'',component:StudentQuestionList},
                    { path: 'question/:pid', component: StudentQuestionPage },
                ]}

            ]}
        ]
    },{
        path:'/apply',component:ApplyListEnter,children:[
            {path:'',component:ApplyList},
        ]
    },
    {
        path:'/addinfo',component:AddList,
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})
router.beforeEach((to, from, next) => {
    const publicPages = ["/", "/main"];
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = localStorage.getItem("access_token");
  
    if (authRequired && !loggedIn) {
      return next("/main");
    } else if (!authRequired && loggedIn) {
      return next();
    } else next();  
  });
export default router
// 路由守卫