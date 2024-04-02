import { shallowMount, createLocalVue } from "@vue/test-utils";
import VueRouter from "vue-router";
import TheAccountView from "@/views/TheAccountView.vue";
import axios from "axios";
import ItemCard from "@/components/ItemCard.vue";
import UserCard from "@/components/UserCard.vue";
import TheProfileView from "@/views/TheProfileView.vue";
import VueI18n from 'vue-i18n';

jest.mock('axios');

jest.mock("@/functions", () => ({
    GeolocationCoords: jest.fn().mockImplementation(() => ({
      longitude: 0,
      latitude: 0,
      update: jest.fn(),
    })),
    formattedDateFromNow : jest.fn().mockImplementation(() => ({

    })),
    ucfirst : jest.fn().mockImplementation(() => ({

    }))
  }));

const i18n = new VueI18n({
    locale: 'fr',
    silentTranslationWarn: true
});

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

// fictive data representing an item
const itemData = {
    category1: "AN",
    category2: "",
    category3: "",
    closed_reason: "",
    comments_count: 0,
    creationdate: "2024-04-02T12:38:54.531979+02:00",
    description: "test description",
    enddate: null,
    id: 10,
    images: [],
    is_closed: false,
    is_recurrent: false,
    location: "SRID=4326;POINT (6.005915786372846 50.63949)",
    name: "test",
    startdate: "2024-04-02T00:00:00+02:00",
    type: "DN",
    use_coordinates: false,
    user: {
        user_id: 4
    },
    views_count: 1,
    visibility: "PB"
};

// Create a local Vue instance for testing
const localVue = createLocalVue();
// Use Vue Router with the local Vue instance
localVue.use(VueRouter);

// Define routes for Vue Router in the application
const routes = [
    // Route for the settings page with a dynamic tab parameter
    { path: '/profile/:id', name: 'profile', component: TheProfileView }
];

// Create a Vue Router instance with the defined routes
const router = new VueRouter({
    routes
});

// Mock de $t
const mocks = {
    $t: key => key, // Mock $t pour simplement retourner la clé
};

describe('test theAccountView', () => {
    it('fetchuser successfully retrieves user data', async () => {
        // Configuring the Axios mock to return dummy data
        axios.get.mockResolvedValue({ data: userData });
    
        // Mount the component
        const wrapper = shallowMount(TheAccountView, { localVue, mocks });
    
        // Wait for API call to end
        await wrapper.vm.fetchUser();
    
        // Check that user data has been correctly assigned
        expect(wrapper.vm.user).toEqual(userData);
    });

    it('fetchItem successfully retrieves item data', async () => {
        // Configuring the Axios mock to return dummy data
        axios.get.mockResolvedValue({ data: itemData });
    
        // Mount the component
        const wrapper = shallowMount(TheAccountView, { localVue, mocks });
    
        // Wait for API call to end
        await wrapper.vm.fetchItems();
    
        // Check that item data has been correctly assigned
        expect(wrapper.vm.items).toEqual(itemData);
    });

    it('test passing props to user-card', async () => {
        const wrapper = shallowMount(UserCard, { localVue,i18n, mocks, propsData: { user: userData } });
        expect(wrapper.props().user).toEqual(userData);

    });

    it('test passing props to item-card', async () => {
        const wrapper = shallowMount(ItemCard, { localVue,i18n, mocks, propsData: { item: itemData } });
        expect(wrapper.props().item).toEqual(itemData);
    });
});
