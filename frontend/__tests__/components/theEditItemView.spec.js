import TheEditItemView from "@/views/TheEditItemView.vue";
import { shallowMount, createLocalVue } from "@vue/test-utils";
import VueRouter from 'vue-router';
import axios from "axios";
import VueI18n from 'vue-i18n';


jest.mock("@/functions", () => ({
    GeolocationCoords: jest.fn().mockImplementation(() => ({
      longitude: 0,
      latitude: 0,
      update: jest.fn(),
      toStringForUser: jest.fn()
    }))
}));

const localVue = createLocalVue()
localVue.use(VueRouter)
const router = new VueRouter()

const mocks = {
    $t: key => key, 
};

const i18n = new VueI18n({
    locale: 'fr',
    silentTranslationWarn: true
});

let wrapper;

jest.mock('axios', () => ({
    patch: jest.fn(),
    post: jest.fn(),
    get: jest.fn()
  }));

describe('Test fetchItem method for TheEditItemView', () => {
    beforeEach(() => {
        wrapper = shallowMount(TheEditItemView,{
            router,
            localVue,
            mocks : mocks,
            i18n,
            
        });
        
        router.push = jest.fn();

        
    });

    it('should fetch item and set fields correctly', async () => {
        const itemId = '123';
        const itemData = {
            name: "Test Item",
            description: "Description of the item",
            startdate: new Date("2024-04-01"),
            enddate: new Date("2024-04-10"),
            use_coordinates: true,
            location: { latitude: 0, longitude: 0 },
        };

        axios.get.mockResolvedValue({ data: itemData });

        // Call fetchItem method
        await wrapper.vm.fetchItem();

        // Assert that item and fields are set correctly
        expect(wrapper.vm.item).toEqual(itemData);

        await wrapper.vm.setFieldFromItem();

        expect(wrapper.vm.internalItem).toEqual(itemData);

    });

    it('should submit form and update item correctly', async () => {

        const itemId = '123';
        const itemData = {
            id: itemId,
            name: "Test Item",
            type: "testType",
            category1: "testCategory1",
            category2: "testCategory2",
            category3: "testCategory3",
            description: "Description of the item",
            startdate: new Date("2024-04-01"), 
            enddate: new Date("2024-04-10"), 
            use_coordinates: true,
            location: { latitude: 0, longitude: 0 },
            visibility: "testVisibility",
            is_recurrent: true
        };
        axios.patch.mockResolvedValue({ data: itemData });
    
        // Mocking images data
        const imageData = {
            files: ['image1.jpg', 'image2.jpg'],
            previews: ['base64_encoded_image1', 'base64_encoded_image2']
        };
        wrapper.setData({ images: imageData });
    
        // Set internalItem data to match the item
        wrapper.setData({ 
            internalItem: {
                name: "John Doe",
                type: "testType",
                category1: "testCategory1",
                category2: "testCategory2",
                category3: "testCategory3",
                description: "Description of the item",
                startdate: new Date("2024-04-01"), 
                enddate: new Date("2024-04-10"), 
                use_coordinates: true,
                location: { latitude: 0, longitude: 0 },
                visibility: "testVisibility",
                is_recurrent: true
            } 
        });
    
        // Call the submit method
        await wrapper.vm.submit();
    
        // Check if waitingFormResponse is set to false after submission
        expect(wrapper.vm.waitingFormResponse).toBe(false);
    
        // Check if router has been pushed to the correct URL
        expect(wrapper.vm.$router.push).toHaveBeenCalledWith(`/items/${itemId}`);
    });
        
});
