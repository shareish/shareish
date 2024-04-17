import TheAddItemView from "@/views/TheAddItemView.vue";
import { shallowMount, createLocalVue } from "@vue/test-utils";
import VueRouter from 'vue-router';
import VueI18n from 'vue-i18n';

jest.mock("@/functions", () => ({
    GeolocationCoords: jest.fn().mockImplementation(() => ({
      longitude: 0,
      latitude: 0,
      update: jest.fn(),
    }))
}));

const mocks = {
    $t: key => key, 
};

const i18n = new VueI18n({
    locale: 'fr',
    silentTranslationWarn: true
});

const localVue = createLocalVue();
localVue.use(VueRouter);
const router = new VueRouter();

describe('TheAddItem.vue', () =>{
    it("test field from addItem form", async () => {
        
        const wrapper = shallowMount(TheAddItemView,{
            mocks : mocks,
            router,
            localVue,
            i18n
        })

        // values that will be transmitted to the fields

        const valueName = "test";;
        const valueAdress = "addresse";
        const valueType = "DN";
        const valueCat1 = "FD";
        const valueCat2 = "EN";
        const valueCat3 = "CH";
        const valueDescription = "This is a test description.";
        const valueStartDate = new Date("2024-04-17T09:50:13.387");
        const valueEndDate = new Date("2024-04-18T09:50:13.387");

        await wrapper.setData({
            name: valueName,
            description: valueDescription,
            type: valueType,
            category1: valueCat1,
            category2: valueCat2,
            category3: valueCat3,
            address: valueAdress,
            startdate: valueStartDate,
            enddate: valueEndDate,
        });

        await wrapper.vm.$nextTick()

        // Convert the Date objects to ISO strings for comparison

        expect(wrapper.find("#name").html()).toContain(valueName);
        expect(wrapper.find("#description").html()).toContain(valueDescription);
        expect(wrapper.find("#type").html()).toContain(valueType);
        expect(wrapper.find("#cat1").html()).toContain(valueCat1);
        expect(wrapper.find("#cat2").html()).toContain(valueCat2);
        expect(wrapper.find("#cat3").html()).toContain(valueCat3);
        expect(wrapper.find("#address").html()).toContain(valueAdress);
        
        // Compare the ISO strings instead of the Date objects
        const startDateReceived = new Date(wrapper.find("#startdate").props("value").toString());
        const endDateReceived = new Date(wrapper.find("#enddate").props("value").toString());

        expect(startDateReceived.getFullYear()).toBe(valueStartDate.getFullYear());
        expect(startDateReceived.getMonth()).toBe(valueStartDate.getMonth());
        expect(startDateReceived.getDate()).toBe(valueStartDate.getDate());

        expect(endDateReceived.getFullYear()).toBe(valueEndDate.getFullYear());
        expect(endDateReceived.getMonth()).toBe(valueEndDate.getMonth());
        expect(endDateReceived.getDate()).toBe(valueEndDate.getDate()); 
        
        expect(wrapper.vm.visibility).toBe('PB');
        expect(wrapper.vm.use_coordinates).toBe(false);
        expect(wrapper.vm.isRecurrent).toBe(false);
        expect(wrapper.vm.images).toEqual([]);
    });
});