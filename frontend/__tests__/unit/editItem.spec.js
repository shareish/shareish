import TheEditItemView from "@/views/TheEditItemView.vue";
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

describe('TheEditItemView.vue', () =>{
    it("test field from addItem form", async () => {
        
        const wrapper = shallowMount(TheEditItemView,{
            mocks : mocks,
            router,
            localVue,
            i18n
        })

        // values that will be transmitted to the fields

        const item = {
            name: "test",
            type: "DN",
            category1: "FD",
            category2: "EN",
            category3: "CH",
            description: "This is a test description.",
            startdate: new Date("2024-04-17T09:50:13.387"),
            enddate: new Date("2024-04-18T09:50:13.387"),
            visibility:'PB'
        };

        const address = "street of test unit, 99 testland";

        await wrapper.setData({
            internalItem : item,
            address: address
        });

        await wrapper.vm.$nextTick();

        expect(wrapper.find("#name").html()).toContain(item.name);
        expect(wrapper.find("#cat1").html()).toContain(item.category1);
        expect(wrapper.find("#cat2").html()).toContain(item.category2);
        expect(wrapper.find("#cat3").html()).toContain(item.category3);
        expect(wrapper.vm.internalItem.type).toBe(item.type);
        expect(wrapper.find("#description").html()).toContain(item.description);
        expect(wrapper.find("#address").html()).toContain(address);
        expect(wrapper.vm.internalItem.isRecurrent).toBe(undefined);

        const startDateReceived = new Date(wrapper.find("#startdate").props("value").toString());
        const endDateReceived = new Date(wrapper.find("#enddate").props("value").toString());

        expect(startDateReceived.getFullYear()).toBe(item.startdate.getFullYear());
        expect(startDateReceived.getMonth()).toBe(item.startdate.getMonth());
        expect(startDateReceived.getDate()).toBe(item.startdate.getDate());

        expect(endDateReceived.getFullYear()).toBe(item.enddate.getFullYear());
        expect(endDateReceived.getMonth()).toBe(item.enddate.getMonth());
        expect(endDateReceived.getDate()).toBe(item.enddate.getDate());
        
        expect(wrapper.vm.internalItem.visibility).toBe('PB');

        expect(wrapper.vm.images.files).toEqual([]);
        expect(wrapper.vm.images.previews).toEqual([]);   
    });
});