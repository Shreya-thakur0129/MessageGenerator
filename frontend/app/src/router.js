import { createRouter, createWebHistory } from "vue-router";
import GenerateMessage from './components/GenerateMessage.vue';

const routes = [
  { path: "/", component: GenerateMessage },
  { path: "/:pathMatch(.*)*", redirect: "/" }
];
      {
        path: "/analytics/conversations",
        component: Analytics,
        name: "DataAnalytics",
      },
      {
        path: "/broadcast/broadcast1",
        component: BroadCast1,
        name: "Broadcast1",
      },
      {
        path: "/broadcast/broadcast2",
        component: BroadCast2,
        name: "Broadcast2",
      },
      {
        path: "/broadcast/broadcast3",
        component: BroadCast3,
        name: "Broadcast3",
      },
      { path: "/contacts/contacts1", component: ContActs1, name: "Contacts1" },
      const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
      {
        path: "/integration/integration1",
        component: AppIntegration,
        name: "Integration1",
      },
      { path: "/profile", component: Profile },
      { path: "/settings", component: Settings },
      { path: "", redirect: "/broadcast/broadcast2" },
      {
        path: "/chatbot/chatbotview",
        component: ChatbotView,
        name: "ChatbotView",
      }, // Updated path
      {
        path: '/generate-message',
        component: GenerateMessage,
        name: 'GenerateMessage',
      },
      // Add more routes within the dashboard as needed
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to check for authentication
// Navigation guard to check for authentication and token expiration
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!token) {
      // No token = not logged in
      
      toast.error("Session expired. Please log in again.");
      return next("/");
    }

    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      const now = Math.floor(Date.now() / 1000);

      if (payload.exp < now) {
        // Token expired
        localStorage.removeItem("token");
        toast.error("Session expired. Please log in again.");
        return next("/");
      }
    } catch (error) {
      // Invalid token format or parsing error
      localStorage.removeItem("token");
      ("Invalid session. Please log in again.");
      return next("/");
    }
  }

  // If route doesn't require auth or token is valid
  next();
});


export default router;
