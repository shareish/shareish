import { shallowMount, createLocalVue, mount} from "@vue/test-utils";
import TheSettingsView from "@/views/TheSettingsView.vue";
import TheSettingsProfile from "@/components/TheSettingsProfile.vue";
import VueRouter from "vue-router";
import axios from "axios";
import TheSettingsAccount from "@/components/TheSettingsAccount.vue";
import TheSettingsNotifications from "@/components/TheSettingsNotifications.vue";


// Create a local Vue instance for testing
const localVue = createLocalVue();
// Use Vue Router with the local Vue instance
localVue.use(VueRouter);

// Define routes for Vue Router in the application
const routes = [
    // Route for the settings page with a dynamic tab parameter
    { path: '/settings/:tab', name: 'settingsTab', component: TheSettingsView }
];

// Create a Vue Router instance with the defined routes
const router = new VueRouter({
    routes
});

// Mock Axios to simulate HTTP calls in tests
jest.mock('axios');



// fictive data representing a user
const userData = {
    first_name: 'John',
    last_name: 'Doe',
    birth_date: '1990-01-01',
    sign_up_date: '2022-04-01',
    email: 'john@example.com',
    username: 'john_doe',
    is_active: true,
    is_admin: false,
    description: 'Lorem ipsum dolor sit amet.',
    homepage_url: 'https://www.example.com',
    facebook_url: 'https://www.facebook.com/johndoe',
    instagram_url: 'https://www.instagram.com/johndoe',
    mastodon_url: 'https://mastodon.social/@johndoe',
    ref_location: null,
    use_ref_loc: false,
    mail_notif_generalinfo: true,
    mail_notif_freq_conversations: 'D',
    mail_notif_freq_events: 'D',
    mail_notif_freq_items: 'D',
    mail_notif_freq_osm: 'W',
    dwithin_notifications: 10,
    save_item_viewing: true,
    is_disabled: false,
    images: []
};

describe("Test de setting view", () => {

    it('fetchuser successfully retrieves user data', async () => {
        
        // Configuring the Axios mock to return dummy data
        axios.get.mockResolvedValue({ data: userData });
    
        // Mount the component
        const wrapper = shallowMount(TheSettingsView,{
            mocks : {
                $t : (key) => {
                    if (key === 'notifications') return 'Notifications';
                }
            },
            localVue,
            router,
            
        });
    
        // Wait for API call to end
        await wrapper.vm.fetchUser();
    
        // Check that user data has been correctly assigned
        expect(wrapper.vm.user).toEqual(userData);
      });
    
    it('test passing props to settings profile', async () => {
        const wrapper = shallowMount(TheSettingsProfile,{
            mocks : {
                $t : (key) => {
                    if (key === '') return '';
                },
                $tc: (key) => {
                    if (key === '') return '';
                },
            },
            propsData:{
                user: userData,
            }
        });

        expect(wrapper.props().user).toEqual(userData);
    });

    it('test passing props to settings Notification', async () => {
        const wrapper = shallowMount(TheSettingsNotifications,{
            mocks : {
                $t : (key) => {
                    if (key === '') return '';
                },
                $tc: (key) => {
                    if (key === '') return '';
                },
            },
            propsData:{
                user: userData,
            }
        });

        expect(wrapper.props().user).toEqual(userData);
    });

    it('test passing props to settings Account', async () => {
        const wrapper = shallowMount(TheSettingsAccount,{
            mocks : {
                $t : (key) => {
                    if (key === '') return '';
                },
                $tc: (key) => {
                    if (key === '') return '';
                },
            },
            propsData:{
                user: userData,
            }
        });

        expect(wrapper.props().user).toEqual(userData);
    });       
});