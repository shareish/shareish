import TheAddItemView from "@/views/TheAddItemView.vue";
import { shallowMount, createLocalVue } from "@vue/test-utils";
import VueRouter from 'vue-router';
import VueI18n from 'vue-i18n';
import axios from "axios";

jest.mock("@/functions", () => ({
    GeolocationCoords: jest.fn().mockImplementation(() => ({
      longitude: 0,
      latitude: 0,
      update: jest.fn(),
    }))
}));

// Mock de $t
const mocks = {
    $t: key => key, 
};

const i18n = new VueI18n({
    locale: 'fr',
    silentTranslationWarn: true
});

const localVue = createLocalVue()
localVue.use(VueRouter)
const router = new VueRouter()

let wrapper;

jest.mock('axios');

describe('test TheAddItemView',() => { 
    beforeEach(() => {
        wrapper = shallowMount(TheAddItemView,{
            mocks : mocks,
            router,
            localVue,
            i18n
        });

        router.push = jest.fn();
    })

    it('test clear address', async () => {
        wrapper.setData({address: "adresse test"});
        expect(wrapper.vm.address).toEqual("adresse test");
        wrapper.vm.clearAddress();
        expect(wrapper.vm.address).toEqual("");
    });

    it('test submit with validation success', async () => {
        // Mocking axios.post to return a successful response
        axios.post.mockResolvedValue({ data: { id: 123 } });

        // Set data values to simulate valid form inputs
        wrapper.setData({
            name: "Test Item",
            type: "DN",
            category1: "PR",
            category2: null,
            category3: null,
            description: "Description of the item",
            address: "Test Address",
            use_coordinates: false,
            isRecurrent: false,
            startdate: new Date(),
            enddate: null,
            visibility: "PB",
            images: [] // Empty images array for simplicity
        });

        // Call the submit method
        await wrapper.vm.submit();

        // Check if the router has been pushed to the correct URL
        expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/items/123');
    });

    it('test submit with validation failure', async () => {
        // Mocking axios.post to return a successful response
        axios.post.mockResolvedValue({ data: { id: 123 } });

        // Set data values to simulate invalid form inputs (e.g., missing name)
        wrapper.setData({
            name: "", // Invalid: name is required
            type: "DN",
            category1: "PR",
            category2: "some_category",
            category3: null,
            description: "Description of the item",
            address: "Test Address",
            use_coordinates: false,
            isRecurrent: false,
            startdate: new Date(),
            enddate: null,
            visibility: "PB",
            images: [] // Empty images array for simplicity
        });

        // Call the submit method
        await wrapper.vm.submit();

        // Check if the router has not been pushed (due to validation failure)
        expect(wrapper.vm.$router.push).not.toHaveBeenCalled();

        // Check if waitingFormResponse is set to false after the submission
        expect(wrapper.vm.waitingFormResponse).toBe(false);
    });

    it('should reset form fields correctly', async () => {
        // Set initial values for the form fields
        wrapper.setData({
            name: 'Test Name',
            description: 'Test Description',
            type: 'Test Type',
            category1: 'Test Category 1',
            category2: 'Test Category 2',
            category3: 'Test Category 3',
            startdate: '2024-04-01',
            enddate: '2024-04-10',
            isRecurrent: true,
            recurrentItem: {
                name: 'Recurrent Item',
                description: 'Recurrent Item Description'
            },
            images: {
                files: ['file1', 'file2'],
                previews: ['preview1', 'preview2']
            }
        });
    
        // Call the resetForm method
        await wrapper.vm.resetForm();
    
        // Assert that form fields are reset to their initial state
        expect(wrapper.vm.name).toBe("");
        expect(wrapper.vm.description).toBe("");
        expect(wrapper.vm.type).toBe('');
        expect(wrapper.vm.category1).toBe('');
        expect(wrapper.vm.category2).toBe('');
        expect(wrapper.vm.category3).toBe('');
        expect(wrapper.vm.startdate).toBe(null);
        expect(wrapper.vm.enddate).toBe(null);
        expect(wrapper.vm.isRecurrent).toBe(false);
        expect(wrapper.vm.recurrentItem).toBe(null);
        expect(wrapper.vm.images.files).toEqual([]);
        expect(wrapper.vm.images.previews).toEqual([]);
    });
    
    it('should clear start date', async () => {
        // Set initial start date as Date object
        wrapper.setData({ startdate: new Date('2024-04-01') });

        // Call the clearStartdate method
        wrapper.vm.clearStartdate();

        // Assert that start date is cleared (null)
        expect(wrapper.vm.startdate).toBe(null);
    });

    it('should clear end date', async () => {
        // Set initial end date as Date object
        wrapper.setData({ enddate: new Date('2024-04-10') });

        // Call the clearEnddate method
        wrapper.vm.clearEnddate();

        // Assert that end date is cleared (null)
        expect(wrapper.vm.enddate).toBe(null);
    });

    it('if the end date is smaller than the start date, the end date is updated', async () => {
        // Set initial start and end dates as Date objects
        wrapper.setData({ startdate: new Date('2024-04-01'), enddate: new Date('2024-04-10') });

        // Call the enddateChanged method
        wrapper.vm.enddateChanged();

        // Assert that start date is updated to match end date
        expect(wrapper.vm.startdate).toEqual(new Date('2024-04-01'));
    });

    it('if the start date is greater than the end date, the end date is updated', async () => {
        // Set initial start and end dates as Date objects
        wrapper.setData({ startdate: new Date('2024-04-10'), enddate: new Date('2024-04-01') });

        // Call the startdateChanged method
        wrapper.vm.startdateChanged();

        // Assert that end date is updated to match start date
        expect(wrapper.vm.enddate).toEqual(new Date('2024-04-10'));
    });
    
});
